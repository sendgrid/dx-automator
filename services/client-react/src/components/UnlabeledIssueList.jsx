import React from 'react';
import {TableBody, TableCell, Table, TableHeader, TableRow, HeaderCell} from "@sendgrid/ui-components"

const UnlabeledIssueList = (props) => {
  return (
    <Table>
      <TableHeader>
        <TableRow>
          <HeaderCell>URL</HeaderCell>
        </TableRow>
      </TableHeader>
      <TableBody>
        { props.unlabeled_issues.map((unlabeled_issue) =>{
          return(
            <TableRow>
              <TableCell className="url">{unlabeled_issue.url}</TableCell>
            </TableRow>
          )
        })}
      </TableBody>
    </Table>

  )
};

export default UnlabeledIssueList;