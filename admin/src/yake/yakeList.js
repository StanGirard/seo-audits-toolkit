import * as React from "react";
import { List,ShowButton,  DeleteButton,Datagrid, TextField, DateField,  } from 'react-admin';
import MyUrlField from '../custom/fields/urlField';



export const YakeList = (props) => (
  <List {...props}
    >
    <Datagrid>
      <TextField source="id" />
      <TextField source="status_job"  label="Type" />
      <DateField source="last_updated"  label="Date"/>
      <ShowButton />
      <DeleteButton undoable={true} />
    </Datagrid>
  </List>
);

