import * as React from "react";
import { TextField,BooleanField, Datagrid, DateField, DeleteButton, List, ShowButton } from 'react-admin';
import MyUrlField from '../custom/fields/urlField';



export const SecurityList = (props) => (
  <List {...props}
    >
    <Datagrid>
      <MyUrlField source="url" />
      <TextField source="score" />
      <BooleanField source="scheduled" />
      <DateField source="last_updated" />
      <ShowButton />
    </Datagrid>
  </List>
);

