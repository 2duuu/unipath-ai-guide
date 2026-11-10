import { describe, it, expect } from "vitest";
import { PackageFeature } from "./packages";

describe("PackageFeature", () => {
  it("has no feature that promises admission probabilities", () => {
    const values = Object.values(PackageFeature) as string[];
    expect(values.some((v) => v.includes("admission") || v.includes("probability"))).toBe(false);
  });

  it("offers the requirements & fit check, mirroring the backend value", () => {
    expect(Object.values(PackageFeature)).toContain("requirements_fit_check");
  });
});
