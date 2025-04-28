# The Sundown Vault

https://2025.archive.plaidctf.com/challenge/2

In `app/src/db.ts`, we can find the ID of the flag:
```
await pool.query(
	sql.unsafe`UPDATE sundown.secret SET secret = ${env.FLAG} WHERE id = '13371337-1337-1337-1337-133713371337'`,
);
```
Once we know the ID, we can focus on the code in `app/src/api.ts`. The server sends a secret as a websocket message if the following function is triggered:
```
	function revealSecret() {
		if (secretId === undefined || secret === undefined) {
			return;
		}

		ws.send(JSON.stringify({ kind: "Reveal", id: secretId, secret }));
		/* [...] */
	}
```
There are exactly two potential usages of above function. The first potential usage happens immediately after fetching the secret from the DB:
```
			const secretData = await pool.maybeOne(sql.type(
				z.object({
					id: z.string(),
					owner_id: z.string(),
					name: z.string(),
					secret: z.string(),
					reveal_at: z.number(),
					created_at: z.number(),
				}),
			)`
				SELECT id, owner_id, name, secret, timestamp_to_ms(reveal_at) AS reveal_at, timestamp_to_ms(created_at) AS created_at
				FROM sundown.secret
				WHERE id = ${data.id}
			`);

			if (secretData === null) {
				ws.send(JSON.stringify({ error: "Secret not found" }));
				return;
			}

			secretId = secretData.id;
			secret = secretData.secret;
			ws.send(JSON.stringify({ kind: "Watch", id: secretId, name: secretData.name }));
			remaining = new Date(secretData.reveal_at).getTime() - Date.now();

			if (remaining <= 0) {
				revealSecret();
			} else {
				if (timeoutDuration === undefined) {
					updateTimeoutDuration();
				}
				updateTimeout();
			}
```
The second potential usage happens from within `updateTimeout`:
```
	function updateTimeout() {
		if (remaining === undefined) {
			return;
		}

		if (timeout !== undefined) {
			clearTimeout(timeout);
		}

		ws.send(JSON.stringify({ kind: "Update", remaining: formatDuration(remaining) }));

		timeout = setTimeout(() => {
			remaining! -= timeoutDuration!;
			if (remaining! <= 0) {
				revealSecret();
			} else {
				updateTimeoutDuration();
				updateTimeout();
			}
		}, timeoutDuration);
	}
```

https://developer.mozilla.org/en-US/docs/Web/API/Window/setTimeout

> Browsers store the delay as a 32-bit signed integer internally. This causes an integer overflow when using delays larger than 2,147,483,647 ms (about 24.8 days).

```
apiRouter.post("/secrets/create", async (req, res) => {
	const body = z
		.object({
			secret: z.string().min(1).max(1000),
			name: z.string().min(1).max(100),
			revealAt: z.string().transform((s, ctx) => {
				const date = DateTime.fromISO(s);

				if (!date.isValid) {
					ctx.addIssue({ code: "custom", message: "Invalid date" });
					return z.NEVER;
				}

				if (s > MaxSecretDate) {
					ctx.addIssue({
						code: "custom",
						message: "Reveal date too far in the future",
					});
					return z.NEVER;
				}

				return date;
			}),
		})
		.parse(req.body);

	if (req.sundown.user === undefined) {
		res.status(403).send("Not authenticated");
		return;
	}

	const id = await pool.oneFirst(sql.type(z.object({ id: z.string() }))`
		INSERT INTO sundown.secret (owner_id, name, secret, reveal_at)
		VALUES (${req.sundown.user}, ${body.name}, ${body.secret}, ms_to_timestamp(${body.revealAt.toMillis()}))
		RETURNING id
	`);

	res.json({ id });
});
```

https://github.com/moment/luxon/blob/e1d9886e478167593217d6621f9a79bc958e89d6/src/impl/regexParser.js#L75

> `const isoYmdRegex = /([+-]\d{6}|\d{4})(?:-?(\d\d)(?:-?(\d\d))?)?/;`
