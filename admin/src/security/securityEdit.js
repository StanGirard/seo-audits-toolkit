import * as React from "react";
import { Edit, SimpleForm, TextInput, DateInput, BooleanInput } from 'react-admin';


export const SecurityEdit = props => (
    <Edit {...props}>
        <SimpleForm>
            <TextInput source="id" />
            <TextInput source="url" />
            <TextInput source="website" />
            <DateInput source="score" />
            <BooleanInput source="scheduled" />
            <DateInput source="last_updated" />
        </SimpleForm>
    </Edit>
);