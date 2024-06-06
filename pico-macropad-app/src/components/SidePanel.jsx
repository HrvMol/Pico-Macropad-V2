import React, { useContext, useState } from 'react';
import { ButtonContext } from '../App'
import FileUpload from './FileUpload';

const SidePanel = () => {
    const [button, setButton] = useContext(ButtonContext)
    const [isMacro, setIsMacro] = useState(true)

    return (
        <div className='w-[33vw] h-[100vh] bg-slate-500 flex items-center flex-col gap-10'>
            <h1 className='text-white text-2xl'>Button: {button}</h1>
            <div className='w-fit'>
                <p>Set Button Type</p>
                <div className='flex flex-row w-full items-center '>
                    <button className='bg-white text-black w-full h-fit px-1 border-2 border-slate-700' onClick={() => setIsMacro(true)}>Macro</button>
                    <button className='bg-white text-black w-full h-fit px-1 border-2 border-slate-700' onClick={() => setIsMacro(false)}>Page</button>
                </div>
            </div>
            <FileUpload />
            <div>{isMacro ? <Macro /> : <Page />}</div>
        </div>
    );
};

const Page = () => {
    return (
        <div className=''>
            <h1>Page</h1>
            <p>link</p>
        </div>
    )
}

const Macro = () => {
    return (
        <div className=''>
            <h1>Macro</h1>
            <p>binding</p>
        </div>
    )
}

export default SidePanel;