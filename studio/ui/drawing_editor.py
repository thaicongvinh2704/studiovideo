"""Interactive editing extensions; the renderer remains independent of the UI."""
import copy
import math

from PySide6.QtCore import Qt, QPointF, QRectF
from PySide6.QtGui import QColor, QPainter, QPen, QPainterPathStroker
from .. import drawing as ink
from .. import drawing_edit as edit


class EditingCanvasMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.zoom = 1.; self.pan = QPointF()
        self.selected = set(); self.node = None; self.active_guide = None
        self.edit_drag = None; self.pan_drag = None
        self.show_guides = True; self.thinning = .35; self.smoothing = .5
        self.tablet_active = False; self.bezier_points = []
        self.guide_name = 'moc'; self.guide_parent = None; self.guide_lock = False

    @property
    def entry(self):
        return self.doc['layers'][self.index]

    def reset_selection(self):
        self.selected.clear(); self.node = None; self.active_guide = None
        self.edit_drag = None; self.bezier_points = []

    def undo(self):
        self.reset_selection(); super().undo()

    def redo(self):
        self.reset_selection(); super().redo()

    def mapping(self):
        scale, x, y = super().mapping()
        base = scale
        scale *= self.zoom
        return scale, x + (base - scale) * self.doc['width'] / 2 + self.pan.x(), y + (base - scale) * self.doc['height'] / 2 + self.pan.y()

    def fit_view(self):
        self.zoom = 1.; self.pan = QPointF(); self.update()

    def wheelEvent(self, event):
        before = self.point(event)
        self.zoom = min(12., max(.2, self.zoom * (1.2 ** (event.angleDelta().y() / 120))))
        scale, x, y = self.mapping()
        self.pan += event.position() - QPointF(x + before.x() * scale, y + before.y() * scale)
        self.update(); event.accept()

    def hit_item(self, point):
        scale = self.mapping()[0]
        for i in range(len(self.entry['items']) - 1, -1, -1):
            item = self.entry['items'][i]
            if item['kind'] == 'text':
                if ink.item_bounds(item).contains(point): return i
            else:
                path = ink.painter_path(item); stroker = QPainterPathStroker()
                stroker.setWidth(max(10 / scale, item.get('width', 3.5)))
                if stroker.createStroke(path).contains(point) or (item.get('fill', 'none') != 'none' and path.contains(point)):
                    return i
        return None

    def current_stroke(self):
        if self.tool == 'brush':
            return edit.brush_item(self.points, self.color, self.size, self.thinning,
                                   self.smoothing, self.tablet_active)
        return super().current_stroke()

    def set_tool(self, tool):
        if self.tool == 'bezier': self.finish_bezier()
        super().set_tool(tool)
        self.node = None

    def finish_bezier(self):
        if len(self.bezier_points) >= 4:
            points = self.bezier_points; commands = [['M', *points[0]]]
            for i in range(1, len(points) - 2, 3):
                commands.append(['C', *points[i], *points[i + 1], *points[i + 2]])
            if self.closed: commands.append(['Z'])
            self.remember()
            self.entry['items'].append(dict(kind='path', commands=commands, stroke=self.color,
                                            fill=self.fill if self.closed else 'none', width=self.size))
            edit.invalidate(self.entry); self.changed.emit()
        self.bezier_points = []; self.update()

    def finish(self):
        if self.tool == 'bezier': self.finish_bezier()
        if self.points: edit.invalidate(self.entry)
        super().finish()

    def paintEvent(self, event):
        p = QPainter(self); p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.fillRect(self.rect(), QColor('#e9edea'))
        scale, x, y = self.mapping(); p.translate(x, y); p.scale(scale, scale)
        rect = QRectF(0, 0, self.doc['width'], self.doc['height'])
        p.fillRect(rect, QColor('white')); p.setClipRect(rect)
        for layer in self.doc['layers']:
            p.save()
            if layer.get('draft'): p.setOpacity(.25)
            ink.paint_layer(p, layer); p.restore()
        if self.points:
            temporary = ink.layer('stroke'); temporary['offset'] = self.entry.get('offset', [0, 0])
            temporary['items'] = [self.current_stroke()]; ink.paint_layer(p, temporary)
        dx, dy = self.entry.get('offset', [0, 0]); p.translate(dx, dy)
        self.selected.intersection_update(range(len(self.entry['items'])))
        p.setBrush(Qt.BrushStyle.NoBrush)
        if self.entry.get('visible', True):
            for i in self.selected:
                item = self.entry['items'][i]
                p.setPen(QPen(QColor('#168d83'), 1 / scale, Qt.PenStyle.DashLine))
                p.drawRect(ink.item_bounds(item).adjusted(-3 / scale, -3 / scale, 3 / scale, 3 / scale))
                if self.tool == 'node':
                    previous = None
                    for ci, c in enumerate(item.get('commands', [])):
                        if c[0] in ('Q', 'C') and previous:
                            p.drawLine(QPointF(*previous), QPointF(c[1], c[2]))
                            p.drawLine(QPointF(*c[-2:]), QPointF(*c[-4:-2]))
                        if len(c) > 1: previous = c[-2:]
                    for ci, ai, pt, knot in edit.point_refs(item):
                        p.setPen(QPen(QColor('#168d83' if knot else '#c48727'), 1 / scale))
                        p.setBrush(QColor('#168d83' if self.node == (i, ci, ai) else 'white'))
                        p.drawEllipse(QPointF(*pt), (4 if knot else 3) / scale, (4 if knot else 3) / scale)
            if self.show_guides:
                guides = {g['id']: g for g in self.entry.get('guides', [])}
                for g in guides.values():
                    p.setPen(QPen(QColor('#b174a0'), 1 / scale, Qt.PenStyle.DashLine))
                    if g.get('parent') in guides:
                        p.drawLine(QPointF(*g['point']), QPointF(*guides[g['parent']]['point']))
                    p.setBrush(QColor('#ae4c8d' if g['id'] == self.active_guide else 'white'))
                    p.drawEllipse(QPointF(*g['point']), 5 / scale, 5 / scale)
                    p.save(); p.translate(*g['point']); p.scale(1 / scale, 1 / scale)
                    p.drawText(QPointF(8, -8), g['name']); p.restore()
        if self.bezier_points:
            p.setPen(QPen(QColor('#168d83'), 1 / scale)); p.setBrush(QColor('white'))
            for a, b in zip(self.bezier_points, self.bezier_points[1:]): p.drawLine(QPointF(*a), QPointF(*b))
            for pt in self.bezier_points: p.drawEllipse(QPointF(*pt), 4 / scale, 4 / scale)
        p.end()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton or (self.tool == 'pan' and event.button() == Qt.MouseButton.LeftButton):
            self.pan_drag = (event.position(), QPointF(self.pan)); return
        if self.tool == 'bezier' and event.button() == Qt.MouseButton.RightButton:
            self.finish_bezier(); return
        if self.tool not in ('select', 'node', 'guide', 'brush', 'bezier'):
            return super().mousePressEvent(event)
        if event.button() != Qt.MouseButton.LeftButton: return
        self.setFocus()
        if not self.entry.get('visible', True) or self.entry.get('locked'): return
        point = QPointF(*self.local(self.point(event))); scale = self.mapping()[0]
        if self.tool == 'brush':
            self.tablet_active = False; self.points = [[point.x(), point.y(), .5]]; self.update(); return
        if self.tool == 'bezier':
            self.bezier_points.append([point.x(), point.y()]); self.update(); return
        if self.tool == 'guide':
            hit = next((g for g in self.entry.get('guides', []) if math.dist(g['point'], [point.x(), point.y()]) < 9 / scale), None)
            if hit:
                self.active_guide = hit['id']; self.remember()
                self.edit_drag = ('guide', copy.deepcopy(self.entry), [point.x(), point.y()])
            else:
                names = {g['name'] for g in self.entry.get('guides', [])}
                name = self.guide_name; suffix = 2
                while name in names: name = self.guide_name + str(suffix); suffix += 1
                self.remember()
                try:
                    self.active_guide = edit.add_guide(self.entry, name, [point.x(), point.y()], self.guide_parent, self.guide_lock)
                except ValueError:
                    self.undo_states.pop(); return
                self.changed.emit()
            self.selection_changed.emit(self.index); self.update(); return
        if self.tool == 'node':
            for i in self.selected:
                for ci, ai, pt, knot in edit.point_refs(self.entry['items'][i]):
                    if math.dist(pt, [point.x(), point.y()]) < 8 / scale:
                        self.node = (i, ci, ai); self.remember()
                        self.edit_drag = ('node', copy.deepcopy(self.entry), [point.x(), point.y()])
                        self.update(); return
        hit = self.hit_item(point)
        if event.modifiers() & Qt.KeyboardModifier.ShiftModifier and hit is not None:
            if hit in self.selected: self.selected.remove(hit)
            else: self.selected.add(hit)
        elif hit not in self.selected:
            self.selected = {hit} if hit is not None else set()
        self.node = None
        if hit is not None and self.tool == 'select':
            bound = any(self.entry['items'][i].get('guide_binding') or self.entry['items'][i].get('node_bindings') for i in self.selected)
            if not bound:
                self.remember(); self.edit_drag = ('items', copy.deepcopy(self.entry), [point.x(), point.y()])
            else:
                self.setToolTip('Nét đang gắn mốc. Dùng công cụ Mốc để kéo mà giữ liên kết.')
        self.selection_changed.emit(self.index); self.update()

    def mouseMoveEvent(self, event):
        if self.pan_drag:
            origin, initial = self.pan_drag
            self.pan = initial + event.position() - origin; self.update(); return
        if self.edit_drag:
            kind, original, origin = self.edit_drag
            self.doc['layers'][self.index] = copy.deepcopy(original)
            pt = self.local(self.point(event))
            if kind == 'node':
                edit.move_node(self.entry, *self.node, pt)
            elif kind == 'guide':
                guide = next(g for g in original['guides'] if g['id'] == self.active_guide)
                edit.move_guide(self.entry, self.active_guide, [guide['point'][j] + pt[j] - origin[j] for j in (0, 1)])
            else:
                for i in self.selected:
                    edit.translate_item(self.entry['items'][i], pt[0] - origin[0], pt[1] - origin[1])
                edit.invalidate(self.entry)
            self.update(); return
        if self.tool == 'brush' and self.points and event.buttons() & Qt.MouseButton.LeftButton:
            pt = self.local(self.point(event))
            if math.dist(pt, self.points[-1][:2]) >= .4: self.points.append([*pt, .5])
            self.update(); return
        if not self.entry.get('locked'): super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.pan_drag:
            self.pan_drag = None; return
        if self.edit_drag:
            self.mouseMoveEvent(event); self.edit_drag = None; self.changed.emit(); return
        if self.tool == 'brush' and self.points:
            self.points.append([*self.local(self.point(event)), .5]); self.finish(); return
        super().mouseReleaseEvent(event)

    def tabletEvent(self, event):
        from PySide6.QtCore import QEvent
        if self.tool != 'brush' or self.entry.get('locked') or not self.entry.get('visible', True):
            event.ignore(); return
        point = [*self.local(self.point(event)), max(.01, event.pressure())]
        if event.type() == QEvent.Type.TabletPress:
            self.tablet_active = True; self.points = [point]
        elif event.type() == QEvent.Type.TabletMove and self.points:
            self.points.append(point)
        elif event.type() == QEvent.Type.TabletRelease and self.points:
            self.finish(); self.tablet_active = False
        self.update(); event.accept()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.bezier_points = []; self.edit_drag = None; self.points = []; self.update(); return
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter) and self.tool == 'bezier':
            self.finish_bezier(); return
        if event.key() == Qt.Key.Key_Delete and self.selected and not self.entry.get('locked'):
            self.remember()
            for i in sorted(self.selected, reverse=True): self.entry['items'].pop(i)
            self.selected.clear(); self.node = None; edit.invalidate(self.entry); self.changed.emit(); return
        if event.key() == Qt.Key.Key_F:
            self.fit_view(); return
        super().keyPressEvent(event)
