import * as React from "react";
import { Datagrid, DateField, List, ShowButton } from 'react-admin';
import MyUrlField from '../custom/fields/urlField';



export const InternalList = (props) => (
  <List {...props}
    >
    <Datagrid>
      <MyUrlField source="url" />
      <DateField source="begin_date" />
      <ShowButton />
    </Datagrid>
  </List>
);

