import React, { useEffect, useState } from "react";
import { EditableMathField } from "react-mathquill";

interface ExpressionBoxProps {
    initialTex: string
    onChange: (tex: string) => void,
    rightAlign?: boolean,
}

export const ExpressionBox: React.FC<ExpressionBoxProps> = ({
    initialTex,
    onChange,
    rightAlign=false,
}) => {
    const [latex, setLatex] = useState<string>(initialTex);

    useEffect(() => {
        setLatex(initialTex);
    }, [initialTex])

    return (
        <EditableMathField
            style={rightAlign ? {textAlign: "right"} : {}}
            className="equationEditor"
            latex={latex}
            onChange={(field) => {
                setLatex(field.latex());
                onChange(field.latex());
            }}
        />
    );
}