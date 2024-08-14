import React, { useMemo, useState } from "react";
import { OrderPanel } from "./OrderPanel"
import { DomainPanel } from "./DomainPanel"
import IntegratorPanel from "./IntegratorPanel"
import { addStyles } from "react-mathquill";
import { FunctionNode, isFunctionNode, isOperatorNode, isSymbolNode, MathNode, OperatorNode, parse, SymbolNode } from "mathjs";
import { parseTex, evaluateTex } from "tex-math-parser";

addStyles();

const renderOrder: Order = ['y', 'z', 'x'];

const isVariable = (node: MathNode, parent: MathNode | undefined): boolean => {
    // https://github.com/josdejong/mathjs/issues/1783
    if (isSymbolNode(node)) {
        if (!parent) return true;
        if (!isFunctionNode(parent)) return true;
        if ((parent as any).name !== node.name) return true;
    }
    return false;
};

// xzy -> zxy // yzx -> zxy
const texFromExpressions = (exprs: Expressions, newOrder: Order) => {
    const texs = renderOrder.map(axis => 
        exprs[axis].map(expr => parse(expr).toTex()) as [string, string],
    )
    const result = {} as Record<XYZ, [string, string]>;
    newOrder.forEach((axis, i) => {result[axis] = texs[i]});
    return result;
};


interface PanelProps {
    order: Order, setOrder: (order: Order) => void,
    exprs: Expressions, setExprs: (exprs: Expressions) => void,
    ranges: Ranges, setRanges: (ranges: Ranges) => void,
    config: DomainConfig, setConfig: (config: DomainConfig) => void,
}

export const Panel: React.FC<PanelProps> = ({
    order, setOrder,
    exprs, setExprs,
    ranges, setRanges,
    config, setConfig,
}) => {
    const [initTex, setInitTex] = useState<Record<XYZ, [string, string]>>(() => texFromExpressions(exprs, order));

    const handleOrderChange = (newOrder: Order) => {
        const tempExprs = {} as Expressions;
        renderOrder.forEach((axis) => {
            tempExprs[axis] = exprs[axis].map(expr => {
                const root = parse(expr).transform((node) => {
                    if (node.type === "SymbolNode") {
                        const idx = renderOrder.indexOf((node as SymbolNode).name as XYZ);
                        if (idx !== -1)
                            return new SymbolNode(newOrder[idx]);
                    }
                    return node;
                })
                return root.toString();
            }) as [Expression, Expression];
        });
        setOrder(newOrder);
        // texFromExpressions(tempExprs, newOrder);
        setInitTex(texFromExpressions(tempExprs, newOrder));
    };

    const handleCodeChange = (axis: XYZ, isUpper: boolean, newTex: string): void => {
        try {
            const root = parseTex(newTex);
            if (root) {
                const allowedSymbols: string[] = order.slice(order.indexOf(axis) + 1)
                const temp = root.transform(node => {
                    if (isOperatorNode(node)) { // remove this shit when refactoring to pass MathNode around instead of expr
                        if (node.op as any === "\\frac") {
                            return new OperatorNode("/", "divide", node.args, node.implicit)
                        }
                    }
                    return node;
                })
                const transformed = temp.transform((node, _, parent) => {
                    if (isVariable(node, parent)) {
                        const sym = (node as SymbolNode).name as XYZ
                        if (!allowedSymbols.includes(sym)) {
                            throw new Error("Invalid symbol");
                        } else {
                            return new SymbolNode(renderOrder[order.indexOf(sym)]);
                        }
                    }
                    return node;;
                });
                const newExprs = structuredClone(exprs);
                newExprs[renderOrder[order.indexOf(axis)]][isUpper ? 1 : 0] = transformed.toString();
                setExprs(newExprs);
            }
        } catch (e) {
            // console.log(e);
        }
    };

    return (
        <div className="panel">
            <OrderPanel order={order} onChange={handleOrderChange}/>
            <DomainPanel
                order={order}
                ranges={ranges} setRanges={setRanges}
                onCodeChange={handleCodeChange}
                initTex={initTex}
                config={config} setConfig={setConfig}
            />
            <IntegratorPanel/>
        </div>
    );
}