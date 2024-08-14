
// type Expression = {
//     code: string
//     valid: boolean,
// }
type Expression = string;
type Expressions = Record<XYZ, [Expression, Expression]>;

type XYZ = 'x' | 'y' | 'z';
type Order = [XYZ, XYZ, XYZ];
type Ranges = Record<XYZ, [number, number]>;
type Domain = {
    y: [(x: number, z: number) => number, (x: number, z: number) => number],
    z: [(x: number) => number, (x: number) => number]
    x: [() => number, () => number]
};
type Axes = Record<XYZ, {min: number, max: number, step: number}>;
type GridXZ = {
    X: Float32Array, // 1D
    Z: Float32Array, // 2D compressed
    numsZ: Int32Array,
    indices: number[],
    reverseIndices: number[],
}

type MeshConfig = {
    transparent: boolean,
    hidden: boolean,
}
type DomainConfig = Record<XYZ, [MeshConfig, MeshConfig]>;

type MeshInfo = {
    vertices: Float32Array,
    normals: Float32Array,
    indices: number[],
};


type LineInfo = {
    vertices: Float32Array,
}

type Config = {
    extendTo3D: boolean,
    
}