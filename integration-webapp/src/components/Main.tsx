import React, { useState, useMemo } from "react"
import { Panel } from "./Panel"
import { Visualiser } from "./Visualiser"
import { parse, compile } from "mathjs";

// TODO domain vs bounds?

const renderOrder: Order = ['y', 'z', 'x'];

// const updateDomain = (domain: Domain, exprs: Expressions, order: Order): void => {
//     const newDomain = {...domain}
//     renderOrder.forEach((axis, i) => {
//         newDomain[axis] = exprs[order[i]]
//     });
// }

const expressionsToDomain = (exprs: Expressions): Domain => {
    const c: any = {
        y: exprs.y.map(expr => compile(expr)),
        z: exprs.z.map(expr => compile(expr)),
        x: exprs.x.map(expr => compile(expr)),
    }
    return {
        y: c.y.map((func: any) => ((x: number, z: number) => func.evaluate({x: x, z: z}))),
        z: c.z.map((func: any) => ((x: number) => func.evaluate({x: x}))),
        x: c.x.map((func: any) => (() => func.evaluate())),
    } as Domain
    // return {
    //     y: exprs.y.map(expr => ((x, z) => compile(expr).evaluate({x: x, z: z}))),
    //     z: exprs.z.map(expr => (x: number) => compile(expr).evaluate({x: x})),
    //     x: exprs.x.map((expr) => () => compile(expr).evaluate()),
    // } as Domain;
};

export const Main: React.FC = () => {
    const [order, setOrder]  = useState<Order>(['y', 'z', 'x']);
    const [exprs, setExprs] = useState<Expressions>({
        // y: ["-1", "1"],
        // z: ["-1", "1"],
        // x: ["-1", "1"],
        y: [
            "-2",
            "cos(sqrt(x^2 + z^2)) + 2"
        ],
        z: [
            "(x^2)/10 - 4",
            "sin(x) + 4",
        ],
        x: [
            "-5",
            "5"
        ],
    });
    const [ranges, setRanges] = useState<Ranges>({
        y: [0, 1],
        z: [0, 1],
        x: [0, 1],
    });

    // const [domain, setDomain] = useState<Domain>();
    const domain = useMemo<Domain>(() => expressionsToDomain(exprs), [exprs])

    const [config, setConfig] = useState<DomainConfig>({
        y: [{ transparent: true, hidden: true }, { transparent: true, hidden: true }],
        z: [{ transparent: false, hidden: true }, { transparent: false, hidden: true }],
        x: [{ transparent: false, hidden: true }, { transparent: false, hidden: true }],
    })

    return (
        <div className="main">
            <Visualiser domain={domain} ranges={ranges} order={order} boundConfig={config} />
            <Panel
                order={order} setOrder={setOrder}
                exprs={exprs} setExprs={setExprs}
                ranges={ranges} setRanges={setRanges}
                config={config} setConfig={setConfig}
            />
        </div>
    )
}
