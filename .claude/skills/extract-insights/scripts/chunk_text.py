import sys
import os

def chunk_text(file_path, chunk_size=4000):
    """
    Reads a text file and splits it into smaller chunks.
    Saves each chunk as a separate file.
    """
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        sys.exit(1)

    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Split by paragraphs or rough character count
    # Simple character count for now, but could be smarter
    chunks = []
    current_chunk = ""

    # Split by lines to avoid cutting sentences
    lines = text.split('\n')

    for line in lines:
        if len(current_chunk) + len(line) < chunk_size:
            current_chunk += line + "\n"
        else:
            chunks.append(current_chunk)
            current_chunk = line + "\n"

    if current_chunk:
        chunks.append(current_chunk)

    # Save chunks
    base_name = os.path.splitext(file_path)[0]
    chunk_files = []

    for i, chunk in enumerate(chunks):
        chunk_file = f"{base_name}_chunk_{i+1}.txt"
        with open(chunk_file, 'w', encoding='utf-8') as f:
            f.write(chunk)
        chunk_files.append(chunk_file)

    # Output list of chunk files separated by newlines
    print("\n".join(chunk_files))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python chunk_text.py <file_path> [chunk_size]")
        sys.exit(1)

    file_path = sys.argv[1]
    chunk_size = int(sys.argv[2]) if len(sys.argv) > 2 else 4000

    chunk_text(file_path, chunk_size)
