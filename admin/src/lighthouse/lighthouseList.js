import * as React from "react";
import { BooleanField, Datagrid, DateField, DeleteButton, List, ShowButton } from 'react-admin';
import MyUrlField from '../custom/fields/urlField';



export const LighthouseList = (props) => (
  <List {...props}
    >
    <Datagrid>
      <MyUrlField source="url" />
      <BooleanField source="scheduled" />
      <DateField source="last_updated" />
      <ShowButton />
    </Datagrid>
  </List>
);

