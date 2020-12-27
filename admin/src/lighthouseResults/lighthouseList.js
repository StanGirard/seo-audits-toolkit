import * as React from "react";
import { Datagrid, DateField, List, ShowButton, TextField } from 'react-admin';
import MyUrlField from '../custom/fields/urlField';
import { LighthouseResultsFilter} from './lighthouseFilter'


export const LighthouseResultsList = (props) => (
  <List {...props}
  filters={<LighthouseResultsFilter />}
  >
    <Datagrid>
      <MyUrlField source="url" />
      <TextField source="accessibility_score" />
      <TextField source="best_practices_score" />
      <TextField source="performance_score" />
      <TextField source="pwa_score" />
      <TextField source="seo_score" />
      <DateField source="timestamp"  showTime="true" />
      <ShowButton />
    </Datagrid>
  </List>
);

