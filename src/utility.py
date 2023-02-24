from typing import Iterator


def format_timestamp(
    seconds: float, always_include_hours: bool = False, decimal_marker: str = "."
):
    """format time stamp for srt file"""
    assert seconds >= 0, "non-negative timestamp expected"
    milliseconds = round(seconds * 1000.0)

    hours = milliseconds // 3_600_000
    milliseconds -= hours * 3_600_000

    minutes = milliseconds // 60_000
    milliseconds -= minutes * 60_000

    seconds = milliseconds // 1_000
    milliseconds -= seconds * 1_000

    hours_marker = f"{hours:02d}:" if always_include_hours or hours > 0 else ""
    return (
        f"{hours_marker}{minutes:02d}:{seconds:02d}{decimal_marker}{milliseconds:03d}"
    )


def write_srt(transcript: Iterator[dict]):
    """
    Write a transcript to a file in SRT format.
    """
    srt_lines = [
        f"{i}\n{format_timestamp(segment['start'], always_include_hours=True, decimal_marker=',')} --> {format_timestamp(segment['end'], always_include_hours=True, decimal_marker=',')}\n{segment['text'].strip().replace('-->', '->')}\n"
        for i, segment in enumerate(transcript, start=1)
    ]
    return "\n".join(srt_lines)
