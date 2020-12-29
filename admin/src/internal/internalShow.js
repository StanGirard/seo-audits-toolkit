import * as React from "react";
import { BooleanField, DeleteButton, EditButton, Show, SimpleShowLayout, TextField } from 'react-admin';
import {Button} from '@material-ui/core';
import { embed } from '@bokeh/bokehjs';
function CreateHTML(record, value) {
    return { __html: record[value] };
}

  



export const InternalShow = (props) => {
    const varia = embed.embed_item(record["result"],'myplot')
    console.log(varia)
    return (
        <Show {...props}>
            <SimpleShowLayout>
                <TextField source="url" />
                <div id='myplot' className="bk-root"></div>
                <EditButton />
                <DeleteButton />
            </SimpleShowLayout>
        </Show>
    )
};

