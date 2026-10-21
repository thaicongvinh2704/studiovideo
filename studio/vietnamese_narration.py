"""Explicit, context-bound reading edits; never guesses how every number is read."""


def apply_readings(original, readings):
    """Return spoken text and an audit trail while preserving the original string.

    Each edit must name exact character offsets, expected source and explanation.
    Offsets always address the unchanged original, including repeated expressions.
    """
    result = []
    audit = []
    cursor = 0
    for entry in sorted(readings, key=lambda item: item['start']):
        start, end = entry['start'], entry['end']
        if not isinstance(start, int) or not isinstance(end, int):
            raise ValueError('Mốc thay cách đọc phải là số nguyên.')
        if start < cursor or end <= start or end > len(original):
            raise ValueError('Các vùng thay cách đọc bị chồng lấn hoặc sai vị trí.')
        if original[start:end] != entry['expected']:
            raise ValueError('Bản gốc đã thay đổi; cần kiểm tra lại cách đọc.')
        if not entry.get('spoken', '').strip() or not entry.get('reason', '').strip():
            raise ValueError('Cần cách đọc và lý do theo ngữ cảnh.')
        result.extend([original[cursor:start], entry['spoken']])
        audit.append(dict(start=start, end=end, original=original[start:end],
                          spoken=entry['spoken'], reason=entry['reason'],
                          context=original[max(0,start-25):min(len(original),end+25)]))
        cursor = end
    result.append(original[cursor:])
    return ''.join(result), audit
