import * as React from "react";
import { List,ShowButton,  DeleteButton,Datagrid, TextField, DateField,  } from 'react-admin';
import MyUrlField from '../custom/fields/urlField';



export const SitemapList = (props) => (
  <List {...props}
    >
    <Datagrid>
      <TextField source="website" />
      <MyUrlField source="url" />
      <TextField source="status_job"  label="Type" />
      <DateField source="begin_date"  label="Date" showTime={true}/>
      <ShowButton />
      <DeleteButton undoable={true} />
    </Datagrid>
  </List>
);

