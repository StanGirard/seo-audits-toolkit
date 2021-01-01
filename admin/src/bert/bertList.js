import * as React from "react";
import { List,ShowButton,  DeleteButton,Datagrid, TextField, DateField, EditButton } from 'react-admin';
import MyUrlField from '../custom/fields/urlField';



export const BertList = (props) => (
  <List {...props}
    >
    <Datagrid>
      <TextField source="summary"  label="Summary" />
      <TextField source="status_job"  label="Result" />
      <DateField source="begin_date"  label="Date"/>
      <ShowButton />
      <DeleteButton undoable={true} />
    </Datagrid>
  </List>
);

