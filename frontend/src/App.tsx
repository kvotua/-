import { useEffect } from "react";
import { AppRoute } from "./app/routes/AppRoute";
import { tg } from "./app/tg";
import { IUser } from "./pages/Profile/Profile";
import { useAppDispatch } from "./app/hooks/useAppDispatch";
import { getUser } from "./app/store/slice/UserSlice/userApi";
import { MenuProvider } from "./app/providers/MenuProvider";
import { ResposeProvider } from "./app/providers/ResponseProvider";

function App() {
  const tgUser: IUser = tg.initDataUnsafe.user; // tgUser - это данные о пользователе, которые беруться с телеграма
  const dispatch = useAppDispatch();

  useEffect(() => {
    tg.ready();
    tg.expand();
    tg.enableClosingConfirmation();
    if (tgUser && tgUser.id) {
      dispatch(getUser(tgUser.id)); // Если tgUser есть - используем его данные, если нет - используются моковые данные
    }
    // Моковые данные
    else {
      dispatch(getUser("0"));
    }
  }, [tgUser]);
  return (
    <>
      <ResposeProvider>
        <MenuProvider>
          <AppRoute />
        </MenuProvider>
      </ResposeProvider>
    </>
  );
}

export default App;
