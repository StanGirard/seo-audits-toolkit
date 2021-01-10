import * as React from "react";
import { Edit, SimpleForm, TextInput, DateInput } from 'react-admin';

export const BertEdit = props => (
    <Edit {...props}>
        <SimpleForm>
            <TextInput source="id" />
            <TextInput source="website" />
            <TextInput source="summary" />
            <TextInput source="text" />
            <TextInput source="result" />
            <TextInput source="status_job" />
            <DateInput source="begin_date" />
        </SimpleForm>
    </Edit>
);