import React from "react";
import { addStyles, StaticMathField } from 'react-mathquill'
import { DndContext, DragEndEvent } from "@dnd-kit/core";
import { arrayMove, horizontalListSortingStrategy, SortableContext } from "@dnd-kit/sortable";
import SortableBox from "./SortableBox"

interface OrderPanelProps {
    order: Order,
    onChange: (order: Order) => void,
}

export const OrderPanel: React.FC<OrderPanelProps> = ({
    order, onChange
}) => {
    const handleDragEnd = (event: DragEndEvent): void => {
        const {active, over} = event;
        if (!over)
            return
        if (active.id !== over.id) {
            const oldIdx = order.indexOf(active.id.toString() as XYZ);
            const newIdx = order.indexOf(over.id.toString() as XYZ);
            onChange(arrayMove(order, oldIdx, newIdx) as Order);
        }
    }

    return (
        <div className="orderPanel">
        <StaticMathField>{"\\int_{\\ }^{\\ }".repeat(3)}</StaticMathField>
        <DndContext onDragEnd={handleDragEnd}>
            <SortableContext
                    items={order}
                    strategy={horizontalListSortingStrategy}
                >
                <div className="orderList">
                    {order.map(coord => <SortableBox key={coord} value={coord}/>)}
                </div>
            </SortableContext>
        </DndContext>
        </div>
    );
};