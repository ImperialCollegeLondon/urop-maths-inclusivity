import React, { useMemo, useState } from "react";
import { ExpressionBox } from "./ExpressionBox"
import RangeSlider from "./RangeSlider"
import { Visibility, VisibilityOff } from "@mui/icons-material";
import { IconButton } from "@mui/material";

const renderOrder: Order = ['y', 'z', 'x'];


interface DomainPanelProps {
    order: Order,
    ranges: Ranges,
    setRanges: (ranges: Ranges) => void,
    onCodeChange: (axis: XYZ, isUpper: boolean, tex: string) => void,
    initTex: Record<XYZ, string[]>,
    config: DomainConfig, setConfig: (config: DomainConfig) => void,
};

export const DomainPanel: React.FC<DomainPanelProps> = ({
    order,
    ranges, setRanges,
    onCodeChange,
    initTex,
    config, setConfig,
}) => {
    const handleRanges = (axis: XYZ, newRange: [number, number]) => {
        setRanges({...ranges, [renderOrder[order.indexOf(axis)]]: newRange} as Ranges);
    };

    const onHiddenClick = (axis: XYZ, i: number): void => {
        const newConfig = structuredClone(config);
        newConfig[axis][i].hidden = !config[axis][i].hidden;
        setConfig(newConfig);
    };

    const rows = order.map((axis, i) => (
        <div className="domainRow" key={axis}>
            <IconButton onClick={() => {onHiddenClick(renderOrder[i], 0)}}>
                {config[renderOrder[i]][0].hidden ? <VisibilityOff /> : <Visibility />}
            </IconButton>
            <ExpressionBox
                initialTex={initTex[axis][0]}
                onChange={((newTex: string) => onCodeChange(axis, false, newTex))}
                rightAlign={true} />
            <RangeSlider values={ranges[renderOrder[i]]} setValues={(newRange: [number, number]) => handleRanges(axis, newRange)} />
            <ExpressionBox
                initialTex={initTex[axis][1]}
                onChange={((newTex: string) => onCodeChange(axis, true, newTex))}
            />
            <IconButton onClick={() => {onHiddenClick(renderOrder[i], 1)}}>
                {config[renderOrder[i]][1].hidden ? <VisibilityOff /> : <Visibility />}
            </IconButton>
        </div>
    ));

    return (
        <div className="domainList">{rows}</div>
    );
}