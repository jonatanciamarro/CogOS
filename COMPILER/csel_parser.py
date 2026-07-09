import re

class CSELParser:
    """
    CSELParser parses CSEL source files containing ENTITY declarations.
    """
    @staticmethod
    def parse(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        entities = {}
        # Matches ENTITY block name and its body
        blocks = re.findall(r"ENTITY\s+(\w+)\s*\{(.*?)\}", content, re.DOTALL)
        
        for name, body in blocks:
            properties = {}
            lines = body.strip().split("\n")
            current_key = None
            
            for line in lines:
                line_clean = line.strip()
                if not line_clean:
                    continue
                if line_clean.endswith(":"):
                    current_key = line_clean[:-1].strip()
                else:
                    if current_key:
                        properties[current_key] = line_clean
                        
            entities[name] = properties
        return entities
