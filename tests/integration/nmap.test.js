const { scan } = require('./helpers')

test(
  "localhost port scan should only find a host finding",
  async () => {
    const { categories, severities, count } = await scan(
      "nmap-localhost",
      "nmap",
      ["localhost"],
      7 * 60
    );

    expect(count).toBe(1);
    expect(categories).toMatchInlineSnapshot(`
      Object {
        "Host": 1,
      }
    `);
    expect(severities).toMatchInlineSnapshot(`
      Object {
        "informational": 1,
      }
    `);
  },
  10 * 60 * 1000
);
