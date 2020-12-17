import * as React from "react";
import { List,ShowButton,  DeleteButton,Datagrid, TextField, DateField, EditButton } from 'react-admin';
import MyUrlField from '../custom/fields/urlField';
import { ExtractorFilter } from './extractorFilter'
export const ExtractorList = (props) => (
  <List {...props}
  filters={<ExtractorFilter />}
    >
    <Datagrid>
      <TextField source="id" />
      <MyUrlField source="url" />
      <TextField source="type_audit" />
      <DateField source="begin_date" />
      <EditButton />
      <ShowButton />
      <DeleteButton undoable={true} />
    </Datagrid>
  </List>
);

