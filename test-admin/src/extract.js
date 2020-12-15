import * as React from "react";
import { List, Datagrid, TextField, DateField, BooleanField } from 'react-admin';
import { Show, SimpleShowLayout, RichTextField, ArrayField } from 'react-admin';

import {
  EditButton,
  ShowButton,
  ReferenceManyField,
  Tab,
  TabbedShowLayout,
} from 'react-admin';


export const ExtractShow = (props) => (
    <Show {...props}>
        <SimpleShowLayout>
            <TextField source="url" />
            <ArrayField source="result">
                <Datagrid>
                    <TextField source="h1" />
                </Datagrid>
            </ArrayField>

            <DateField label="Publication date" source="begin_date" />
        </SimpleShowLayout>
    </Show>
);

export const ExtractList = (props) => (
    <List {...props}>
        <Datagrid>
            <TextField source="id" />
            <TextField source="url" />
            <TextField source="type_audit" />
            <TextField source="status_job" />
            <DateField source="begin_date" />
        </Datagrid>
    </List>
);



export const PostShow = props => (
  <Show {...props}>
    <TabbedShowLayout>
      <Tab label="Summary">
        <TextField source="id" />
        <TextField source="title" />
        <TextField source="teaser" />
      </Tab>
      <Tab label="Body" path="body">
        <RichTextField
          source="body"
          stripTags={false}
          label=""
          addLabel={false}
        />
      </Tab>
      <Tab label="Comments" path="comments">
        <ReferenceManyField
          addLabel={false}
          reference="comments"
          target="post_id"
          sort={{ field: 'created_at', order: 'DESC' }}
        >
          <Datagrid>
            <DateField source="created_at" />
            <TextField source="body" />
            <ShowButton />
            <EditButton />
          </Datagrid>
        </ReferenceManyField>
      </Tab>
    </TabbedShowLayout>
  </Show>
);
