import { useContext, useEffect } from "react";
import { menuContext } from "../context";
import { IMenu } from "src/widgets/Menu/MenuModel";

export const useChangeMenu = (menuItem: IMenu[]) => {
  const { setMenuItems } = useContext(menuContext);
  useEffect(() => {
    setMenuItems(menuItem);
  }, []);
};
