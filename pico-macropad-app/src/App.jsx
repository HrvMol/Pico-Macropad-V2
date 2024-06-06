import { createContext, useState } from "react";
import { Grid, SidePanel } from "./components";

export const ButtonContext = createContext();

const App = () => {
  const [button, setButton] = useState(1);
  
  return (
    <ButtonContext.Provider value={[button, setButton]}>
      <div className="flex justify-end">
        <div className="w-full flex justify-center items-center">
          <Grid />
        </div>
        <SidePanel />
      </div>
    </ButtonContext.Provider>
  );
}

export default App;