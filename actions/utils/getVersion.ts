import { Context } from "@actions/github/lib/context";

const REF_REGEX = /^refs\/(.+?)\/(.+)$/;

export default function getVersion(context: Context): string {
  const [ref, refType, refName] = context.ref.match(REF_REGEX) || [];

  if (!ref) {
    throw new Error(`Invalid ref: ${context.ref}`);
  }
  if (refType !== "tags") {
    throw new Error(`Invalid ref type, must be "tags": ${refType}`);
  }

  return refName;
}
