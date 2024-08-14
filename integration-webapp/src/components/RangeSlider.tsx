import React from "react";
import Box from "@mui/material/Box";
import Slider from "@mui/material/Slider";

const minDistance = 0.001;

interface RangeSliderProps {
    values: [number, number],
    setValues: (newValues: [number, number]) => void,
}

export default function RangeSlider({values, setValues}: RangeSliderProps) {
    const handleChange = (
        event: Event,
        newValue: number | number[],
        activeThumb: number,
    ) => {
        if (!Array.isArray(newValue)) {
            return;
        }
    
        if (activeThumb === 0) {
            setValues([Math.min(newValue[0], values[1] - minDistance), values[1]]);
        } else {
            setValues([values[0], Math.max(newValue[1], values[0] + minDistance)]);
        }
    };

    return (
        <Box sx={{ width: 100 }}>
            <Slider
                value={values}
                min={0}
                step={0.01}
                max={1}
                onChange={handleChange}
                disableSwap
                sx={{
                    "& .MuiSlider-track": {
                        color: "#0000cd",
                    },
                    "& .MuiSlider-thumb": {
                        borderRadius: 0,
                        width: "5px",
                        color: "#0000cd",
                    }
                }}
            />
        </Box>
    )
}