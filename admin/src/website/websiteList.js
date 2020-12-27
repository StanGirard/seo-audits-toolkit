import * as React from "react";
import { Datagrid, DeleteButton, List, TextField } from 'react-admin';
import MyUrlField from '../custom/fields/urlField';


export const WebsiteList = (props) => (
  <List {...props}
//   filters={<ExtractorFilter />}
    >
    <Datagrid>
      <TextField source="name" />
      <MyUrlField source="url" />
      <DeleteButton undoable={true} />
    </Datagrid>
  </List>
);