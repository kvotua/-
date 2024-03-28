import { Dispatch, SetStateAction, createContext } from "react";
import { IMenu } from "src/widgets/Menu/MenuModel";
import { menuItem } from "../routes/menuListItem";

interface IMenuContext {
  menuItems: IMenu[];
  setMenuItems: Dispatch<SetStateAction<IMenu[]>>;
}

interface IResponseContext {
  response: {
    errorMessage?: string;
    refetchFunc?: () => void;
    isLoading?: boolean;
    isSuccess?: boolean;
  };
  setResponse: React.Dispatch<
    React.SetStateAction<{
      errorMessage?: string;
      refetchFunc?: () => void;
      isLoading?: boolean;
      isSuccess?: boolean;
    }>
  >;
}

export const menuContext = createContext<IMenuContext>({
  menuItems: menuItem,
  setMenuItems: () => {},
});
export const responseContext = createContext<IResponseContext>({
  response: {
    errorMessage: "",
    refetchFunc: () => {},
    isLoading: false,
    isSuccess: false,
  },
  setResponse: () => {},
});
