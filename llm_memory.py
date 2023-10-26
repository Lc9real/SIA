import os

class Memory_System():
    def __init__(self, MemoryKey:str):
        self.memory_key = MemoryKey
        f = open(f"{self.memory_key}.memory", "a")
        f.close()

    def load_Memory(self) -> str:
        f = open(f"{self.memory_key}.memory", "r")
        content = f.read()
        f.close()
        return content


    def add_Memory(self, username:str, input:str, output:str):
        f = open(f"{self.memory_key}.memory", "a")
        f.write(f"\n{username}: {input}\nSIA: {output}")
        f.close()

    def clear_Memory(self):
        os.remove(f"{self.memory_key}.memory")
        f = open(f"{self.memory_key}.memory", "a")
        f.close()



