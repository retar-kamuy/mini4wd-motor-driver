// Simple BLE command queue placeholder
// Manages sequential execution of async BLE commands.

type CommandFn = () => Promise<any>;

export class BleQueue {
  private queue: CommandFn[] = [];
  private running = false;

  /** Add a command to the queue. Returns a promise that resolves with the command result. */
  enqueue<T>(cmd: () => Promise<T>): Promise<T> {
    return new Promise<T>((resolve, reject) => {
      this.queue.push(async () => {
        try {
          const result = await cmd();
          resolve(result);
        } catch (e) {
          reject(e);
        }
      });
      this.runNext();
    });
  }

  private async runNext() {
    if (this.running) return;
    const next = this.queue.shift();
    if (!next) return;
    this.running = true;
    try {
      await next();
    } finally {
      this.running = false;
      // continue processing remaining items
      this.runNext();
    }
  }
}

