import { describe, expect, test } from "@jest/globals";
import { Context } from "@actions/github/lib/context";
import getVersion from "./getVersion";

describe("getVersion", () => {
  test("parses a tag ref properly", () => {
    const context = { ref: "refs/tags/1.2.3" } as Context;

    const version = getVersion(context);
    expect(version).toEqual("1.2.3");
  });

  test("throws on branch refs", () => {
    const context = { ref: "refs/heads/main" } as Context;

    expect(() => getVersion(context)).toThrow("Invalid ref");
  });

  test("throws on bad refs", () => {
    const context = { ref: "bad-ref" } as Context;

    expect(() => getVersion(context)).toThrow("Invalid ref");
  });
});
