
## 📂 File Sorter Node
Your automated digital librarian, designed to bring order to the creative chaos of your output folder by sorting files into categorized subfolders.

Philosophy & Use Case: The File Sorter Node is a powerful housekeeping utility that tackles the ever-growing clutter in your output directory. As you generate hundreds of images, videos, and other assets, this node automates the process of organizing them. It operates with a "safety-first" principle: by default, it performs a "dry run," showing you exactly what it plans to do without moving a single file. This allows you to verify its logic before committing to the sort.

General Usage: The node's primary function is to scan a target directory and move files into subfolders based on their extension.

target_folder: The main directory you want to organize (e.g., your ComfyUI output folder).

image_extensions / video_extensions: Pre-defined, comma-separated lists for sorting common image and video files into Images and Videos subfolders.

other_mappings: A powerful feature allowing you to define your own custom sorting rules. For example, Audio:.mp3,.wav would create an Audio folder for your sound files.

execute_sort: This is the most important control. It is False by default. While False, the node will only output a report of the files it found and where it would move them. You must toggle this to True for the node to actually move the files.

<img width="476" height="329" alt="image" src="https://github.com/user-attachments/assets/9b192a64-ca89-4972-9292-5a7fe4e29058" />


## 📂 Media Migrator Node
A powerful logistics tool for moving entire media libraries from a source folder to a new destination drive, while perfectly preserving the original folder structure.

Philosophy & Use Case: The Media Migrator is your digital moving truck. It's designed for large-scale organization tasks, such as moving your entire output folder from a nearly full SSD to a large archival hard drive. It intelligently scans for all image and video files, recreates their original folder hierarchy on the new drive (within a container folder named _Moved_media), and then moves them. Like the File Sorter, it operates with a "dry run" safety feature, telling you what it will do before it does anything.

General Usage:

source_folder: The root folder containing all the media you want to move.

destination_drive: The drive you want to move the media to (e.g., D:\).

execute_move: The critical safety switch. It defaults to False, providing a preview of the operation. You must set this to True for the node to actually move the files.

<img width="333" height="173" alt="image" src="https://github.com/user-attachments/assets/a8d06d98-4cd1-4342-bedd-5fc119ea52f3" />


## 📂 Empty Folder Cleaner
A housekeeping utility that recursively scans a directory and deletes any empty folders it finds, keeping your project directories clean and organized.

Philosophy & Use Case: The Empty Folder Cleaner is your automated janitor. After large projects or extensive sorting with the File Sorter, you're often left with a skeleton of empty directories. This node sweeps through your target folder and removes them. It operates with a crucial "dry run" safety feature: by default, it will only report on the empty folders it finds. You must explicitly tell it to perform the deletion.

General Usage:

target_folder: The root directory you want to clean up.

execute_cleanup: The safety switch. By default, this is False, and the node will only output a list of empty folders it has found. To actually delete the folders, you must toggle this to True.

<img width="412" height="224" alt="image" src="https://github.com/user-attachments/assets/10d86016-3e8e-46c5-b088-309fe3b8c77d" />


## 📂 Load Batch Images Dir (Full Batch Loader)
A powerful batch loader designed to load a complete set of images from a directory into a single batch, perfect for tasks like dataset preparation or processing a collection of images at once.

Philosophy & Use Case: This is your bulk-loading specialist. Use this node when you need to load an entire folder of images (or a specific slice of it) into a single stack for processing. It's highly efficient, with built-in caching and image validation to skip corrupted files. It's the ideal tool for starting any workflow that needs to operate on a collection of images simultaneously. If the images are different sizes, it will intelligently resize subsequent images to match the dimensions of the first one.

General Usage:

directory: The folder containing the images you want to load.

image_load_cap: The maximum number of images to load. A value of 0 means it will load all valid images.

start_index: The position in the alphabetically sorted list of files from which to start loading. This allows you to skip the first 'N' images.

force_rescan: By default, the node caches the file list for speed. Toggle this to True if you've added or removed files and need the node to see the changes.

<img width="370" height="257" alt="image" src="https://github.com/user-attachments/assets/46b27d98-f5bd-42ab-a5d1-39d27cfb6f71" />


## 📂 Load Batch From Dir (Sequential/Iterative Loader)
An intelligent, stateful loader designed to load a single image from a directory, remembering its position for the next run. This is the engine for building looping workflows.

Philosophy & Use Case: This node is your workflow's memory. Despite the name, it's not a "batch" loader in the traditional sense; it's an iterator. Its core genius is the increment mode, which loads one image, then on the next run, automatically loads the next one in the sequence. It's the essential tool for building automated loops that process a folder of images one by one, for example, in a batch img2img process.

General Usage:

A Note on Naming: This node may share a display name with the "Full Batch Loader." The key functional difference is that this one has an iteration_mode input.

directory: The folder containing the images to iterate through.

iteration_mode:

increment: The primary mode. Loads the next image in the sequence on each run.

fixed: Always loads the first image in the folder.

random: Loads a random image on each run.

trigger: This optional input is a "poker." It doesn't use the data connected to it, but connecting any changing output (like a counter) will force the node to re-run, which is essential for building automated loops.

<img width="401" height="213" alt="image" src="https://github.com/user-attachments/assets/a6913d16-593d-4330-8cde-e592bcf0e776" />


## 📂 Load Video Path
A comprehensive node for loading video files and extracting their image frames, audio, and metadata for use in a workflow.

Philosophy & Use Case: This node is the primary entry point for any workflow that processes an existing video file. It's designed to give you precise, granular control over exactly which frames are loaded into memory. This is essential for managing VRAM, creating loops that process a video in chunks, or selecting specific segments for an img2img video workflow.

General Usage:

video: The file path to the video you want to load.

Frame Selection Controls (frame_load_cap, start_at_frame, select_every_nth): These are the most important controls. They act as your "slicing" tools, allowing you to specify exactly which portion of the video to load (e.g., "load 100 frames, starting at frame 300, and only take every 2nd frame").

Outputs: The node provides everything needed for a complete video workflow: a batch of IMAGE frames, the total frame_count (useful for looping logic), and the audio track for separate processing.

<img width="399" height="362" alt="image" src="https://github.com/user-attachments/assets/377c33a6-23ed-46a9-bad3-f0ae7637bd93" />


## 📂 Sanitize Filename
An essential utility node that cleans and sanitizes a string of text, making it safe to use as a filename on any operating system.

Philosophy & Use Case: The Sanitize Filename node is your digital proofreader. Operating systems have strict rules about what characters are allowed in a filename (\, /, :, *, ?, ", <, >, | are all forbidden). This node acts as a filter, taking any text—especially AI-generated text which can be unpredictable—and stripping out all illegal characters and extra spaces. It's a crucial final step before any "Save" operation to prevent errors and ensure your files are saved correctly every time.

General Usage: You connect any text string to the text input. The node outputs a clean, safe sanitized_text string that can be used as a filename prefix or a full filename.

<img width="446" height="295" alt="image" src="https://github.com/user-attachments/assets/8b7e3613-b307-48d7-bd97-6163175bea7d" />

