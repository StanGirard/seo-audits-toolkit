import * as React from "react";
import { SimpleShowLayout,Show, TextField} from 'react-admin';

export const ExtractorShow = (props) => (
  <Show {...props}>
      <SimpleShowLayout>
          <TextField source="url" />
          <TextField source="type_audit" />
          <TextField source="result" />
      </SimpleShowLayout>
  </Show>
);
