## UI for Transcriptions, Summaries & Analytics

---

#### Run Transcription

- Select a local file on the left
- If you want to trim the clip, you can add a start timestamp and/or duration (leaving duration at a negative value will trim to the end of the clip)
- Click "Transcribe"
  This will replace these instructions with transcriptions along with A/V on the Transcribe page. Not to worry, they'll still be on the help page if needed.

Once a transcription is created, it will be retained as a session variable so you can navigate around.
**Note:** If you refresh or add a new file, the old transcription will be replaced.

---

#### Run Summarizers

- On the Summary page, pick a summarization model from [Hugging Face](https://huggingface.co/models?pipeline_tag=summarization&sort=downloads) and click "Run Summarization"
