import React, { useEffect, useMemo, useRef } from "react"
import { Canvas } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import * as utils from "../utils";
import { BufferAttribute, BufferGeometry, DoubleSide, FrontSide, BackSide, Group, Mesh, MeshStandardMaterial, Matrix4, MeshNormalMaterial } from "three";

// run on init

// const config = {
//     extendTo3D: false,
//     domainConfig: boundConfig,
// };

interface VisualiserProps {
    domain: Domain,
    ranges: Ranges,
    order: Order,
    boundConfig: DomainConfig,
}

const bases: Record<XYZ, number[]> = {
    x: [1, 0, 0, 0],
    y: [0, 0, -1, 0],
    z: [0, 1, 0, 0],
}

const isMeshInfo = (x: any): x is MeshInfo => x.indices !== undefined;

export const Visualiser: React.FC<VisualiserProps> = ({
    domain,
    ranges,
    order,
    boundConfig,
}) => {
    const volumeGeometry = useMemo<BufferGeometry[]>(
        () => {
            const idomain = utils.interpolateDomain(domain, ranges);
            return utils.createVolume(idomain).map(info => {
                const geometry = new BufferGeometry();
                geometry.setIndex(info.indices);
                geometry.setAttribute("position", new BufferAttribute(info.vertices, 3));
                geometry.setAttribute("normal", new BufferAttribute(info.normals, 3));
                return geometry;
            });
        },
        [domain, ranges],
    );

    const EPS = 0.05;
    const boundaryGeometry = useMemo<{g: BufferGeometry, isMesh: boolean}[]>(
        () => {
            const d: Domain = {
                y: [(x: number, z: number) => domain.y[0](x, z)-EPS, (x: number, z: number) => domain.y[1](x, z)+EPS],
                z: [(x: number) => domain.z[0](x), (x: number) => domain.z[1](x)],
                x: [() => domain.x[0](), () => domain.x[1]()],
            }
            return utils.createBoundary(d).map(info => {
                const geom = new BufferGeometry();
                geom.setAttribute("position", new BufferAttribute(info.vertices, 3));
                if (isMeshInfo(info)) {
                    geom.setIndex(info.indices);
                    geom.setAttribute("normal", new BufferAttribute(info.normals, 3));
                }
                return {g: geom, isMesh: isMeshInfo(info)};
            })
        }, [domain]
    );

    const matrix: Matrix4 = useMemo<Matrix4>(
        () => {
            const a: number[] = [];
            a.push(...bases[order[2]]);
            a.push(...bases[order[0]]);
            a.push(...bases[order[1]]);
            a.push(...[0, 0, 0, 1]);
            return (new Matrix4()).fromArray(a);
        },
        [order],
    );

    return (
        // TODO use useThree() for width and height
        <Canvas orthographic camera={{zoom: 50, position: [0, 3, 15]}}>
            <ambientLight intensity={1} />
            <pointLight intensity={100} position={[-10, 15, -10]} />
            <pointLight intensity={100} position={[5, 10, 5]} />
            {volumeGeometry.map((geometry, i) => 
                <mesh key={i} geometry={geometry} matrix={matrix} matrixAutoUpdate={false}>
                    {/* <meshStandardMaterial color={0x6655ff} side={DoubleSide}/> */}
                    <meshNormalMaterial side={DoubleSide}/>
                    {/* <meshBasicMaterial wireframe /> */}
                </mesh>
            )}
            {boundaryGeometry.map((obj, i) => {
                const conf = boundConfig[(['y', 'y', 'z', 'z', 'x', 'x'] as XYZ[])[i]][i % 2];
                if (!conf.hidden) {
                    if (obj.isMesh) {
                        return (
                            <mesh key={i} geometry={obj.g} matrix={matrix} matrixAutoUpdate={false}>
                                <meshStandardMaterial color={0x6655ff} side={DoubleSide} transparent={conf.transparent} opacity={0.3}/>
                            </mesh>
                        )
                    } else {
                        return (
                            //@ts-ignore
                            <line key={i} geometry={obj.g} matrix={matrix} matrixAutoUpdate={false}>
                                <lineBasicMaterial color={0x000000} />
                            </line>
                        )
                    }
                }
            })}

            <OrbitControls />
        </Canvas>
    );
};