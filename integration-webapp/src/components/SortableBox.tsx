import React from "react";
import { CSS } from "@dnd-kit/utilities"
import { useSortable } from "@dnd-kit/sortable";
import { StaticMathField } from 'react-mathquill'

export default function SortableBox({value}: {value: string}) {
    // TODO disable accidental selection of latex
    const {attributes, listeners, setNodeRef, transform, transition} = useSortable({id: value});

    const style = {
        transform: CSS.Transform.toString(transform),
        transition,
    }

    return (
        <div ref={setNodeRef} style={style} {...attributes} {...listeners}>
            <StaticMathField>{"\\mathrm{d}" + value}</StaticMathField>
        </div>
    );
}