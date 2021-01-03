import * as React from "react";
import { Datagrid, DateField, List, ShowButton, TextField } from 'react-admin';
import MyUrlField from '../custom/fields/urlField';
import { SecurityResultsFilter} from './securityFilter'


export const SecurityResultsList = (props) => (
  <List {...props}
  filters={<SecurityResultsFilter />}
  >
    <Datagrid>
      <MyUrlField source="url" />
      <TextField source="score" />
      <DateField source="timestamp"  showTime="true" />
      <ShowButton />
    </Datagrid>
  </List>
);

