import * as React from "react";
import { DeleteButton, EditButton, Show, SimpleShowLayout, TextField } from 'react-admin';
import MyUrlField from '../custom/fields/urlField';
export const SecurityResultsShow = (props) => {

    return (
        <Show {...props}>
            <SimpleShowLayout>
                <MyUrlField source="url" />
                <TextField source="score" />
                <TextField source="result" />
                <EditButton />
                <DeleteButton />
            </SimpleShowLayout>
        </Show>
    )
};
