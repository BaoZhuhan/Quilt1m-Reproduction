# Quilt1m-Reproduction

## Reproduction of Quilt1m

I have successfully reproduced the Quilt1m project by following the [original Repo](https://github.com/wisdomikezogwo/quilt1m) and correcting some code errors. The demo image-text pair data generated is located at:

## Script Descriptions

- trans.py: Converts .webm, .mkv, or .webp files to .mp4 format using moviepy.

- autorename.py: Recursively traverses directories to rename video files and invokes trans.py on non-mp4 files.

- Inference_extraction.py: Analyzes text files and extracts causal or inferential sentences using OpenAI's API.
