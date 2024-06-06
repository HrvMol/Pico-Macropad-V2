import React, { useContext } from 'react'
import { ButtonContext } from '../App'

const Grid = () => {
    const [button, setButton] = useContext(ButtonContext)

    const width = 3; // Replace with desired width
    const height = 3; // Replace with desired height

    const renderGrid = () => {
        const grid = [];
        for (let row = 0; row < height; row++) {
            const rowItems = [];

            for (let col = 0; col < width; col++) {
                let key = row * width + col + 1;
                rowItems.push(<button key={key} className="grid-item w-20 h-20 inline-block bg-black" onClick={() => setButton(key)}></button>);
            }

            grid.push(<div key={row} className="flex flex-row gap-2">{rowItems}</div>);
        }

        return grid;
    };

    return (
        <div className="flex flex-col gap-2">
            {renderGrid()}
        </div>
    );
};

export default Grid;