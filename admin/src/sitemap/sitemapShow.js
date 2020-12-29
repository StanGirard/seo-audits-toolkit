import * as React from "react";
import { ArrayField, Datagrid, DateField, DeleteButton, EditButton, Show, SimpleShowLayout, TextField, UrlField } from 'react-admin';

export const SitemapShow = (props) => {

    return (
        <Show {...props}>
            <SimpleShowLayout>
                <TextField source="id" />
                <TextField source="url" />
                <ArrayField source="result" fieldKey="id">
                    <Datagrid>
                        <UrlField source="url" />
                        <DateField source="last_modified" showTime={true}/>
                    </Datagrid>
                </ArrayField>
                <EditButton />
                <DeleteButton />
            </SimpleShowLayout>
        </Show>
    )
};