import * as React from "react";
import { BooleanField, DeleteButton, EditButton, Show, SimpleShowLayout, TextField } from 'react-admin';

export const SecurityShow = (props) => {
    
    return (
    <Show {...props}>
        <SimpleShowLayout>
            <TextField source="url" />
            <BooleanField source="scheduled" />
            <TextField source="score" />
            <EditButton/>
            <DeleteButton />
        </SimpleShowLayout>
    </Show>
)};
