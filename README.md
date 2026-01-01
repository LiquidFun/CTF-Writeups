# CTF-Writeups

Our solutions and write-ups to various CTFs for team "Never :q!". We are quite a newbie team, don't expect many solves. This is more of a reference for future CTFs as well as a write-up of learnings for each challenge.

## CTFs participated in 

| Event/CTF | Year | Solved | Place | 
| --- | --- | --- | --- |
| [Telnet - Klartext Reden @ 39C3](https://events.ccc.de/congress/2025/hub/de/assembly/detail/telnet-klartext-reden) | 2025 | 9/9 | 35/200 |
| [Hack.lu](https://2025.hack.lu/ctf/)^[ctftime](https://ctftime.org/event/2842) | 2025 | 14/33 | 43/299 |
| [PlaidCTF](https://plaidctf.com/)^[ctftime](https://ctftime.org/event/2508) | 2025 | 5/18 | 40/903 |
| [Telnet - Klartext Reden @ 38C3](https://events.ccc.de/congress/2024/hub/en/assembly/telnet-klartext-reden/) | 2024 | 9/9 | ? |
| [Hack.lu](https://2024.hack.lu/ctf/)^[ctftime](https://ctftime.org/event/2438) | 2024 | 3/? | 56/155 |

## Write-ups Overview

| Event | Challenge | Category | Points | Description | 
| --- | --- | --- | --- | --- | 
| [39C3](https://events.ccc.de/congress/2025/hub/de/assembly/detail/telnet-klartext-reden) | [Telnet - Klartext Reden](./39C3/TelnetChallenge/) | misc | - | Decipher I2C signal from cat video, decode hints from braille posters and brute force keepass argon2 password and many more |
| [PlaidCTF-2025](https://plaidctf.com/) | [Prospectin'](PlaidCTF-2025/Prospectin) | rev | p1:100 p2:250 | Given binary, decompile: contains hundreds of ifs which directly use parts of the flag to compute a score. Convert ifs to z3; maximize score. |
| [PlaidCTF-2025](https://plaidctf.com/) | [Plaid Apple](PlaidCTF-2025/PlaidApple) | misc | 175 | Given only a video of noise, with movement only perceivable when viewing as video. Extract QR codes in the difference of adjacent frames, QR codes contain single letters, which include the flag |

