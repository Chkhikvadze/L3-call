import { ButtonPrimary } from 'components/Button/Button'
import ComponentsWrapper from 'components/ComponentsWrapper/ComponentsWrapper'
import DataGrid from 'components/DataGrid'
import HeaderComponent from 'components/DataGrid/GridComponents/HeaderComponent'

import IconButton from '@l3-lib/ui-core/dist/IconButton'

import {
  StyledHeaderGroup,
  StyledSectionTitle,
  StyledSectionWrapper,
} from 'pages/Home/homeStyle.css'
import TextCellRenderer from 'pages/TeamOfAgents/TeamOfAgentsTable/TextCellRenderer'
import { useMemo } from 'react'

import { useNavigate } from 'react-router-dom'

import { useGroups } from './useGroups'
import {
  StyledDeleteIcon,
  StyledEditIcon,
} from 'pages/TeamOfAgents/TeamOfAgentsCard/TeamOfAgentsCard'
import styled from 'styled-components'

const Groups = () => {
  const { groups, deleteGroupHandler } = useGroups()

  const navigate = useNavigate()

  const gridData =
    groups?.map((group: any) => ({
      id: group.id,
      name: group.name,
      description: group.description,
    })) || []

  const config = useMemo(
    () => [
      {
        headerName: 'Name',
        field: 'name',
        headerComponent: HeaderComponent,

        resizable: true,
        cellRenderer: TextCellRenderer,
        minWidth: 200,
        width: 350,
        flex: 2,
      },
      {
        headerName: 'Description',
        field: 'description',
        headerComponent: HeaderComponent,

        resizable: true,
        cellRenderer: TextCellRenderer,
        minWidth: 200,
        width: 350,
        flex: 2,
      },
      {
        headerName: '',
        field: 'id',
        headerComponent: (p: any) => <div></div>,
        cellRenderer: (p: any) => {
          const { value: id } = p
          return (
            <StyledTableButtons>
              <IconButton
                onClick={() => deleteGroupHandler(id)}
                icon={() => <StyledDeleteIcon />}
                size={IconButton.sizes.SMALL}
                kind={IconButton.kinds.TERTIARY}
                // ariaLabel='Delete'
              />

              <IconButton
                onClick={() => navigate(`/groups/${id}/edit-group`)}
                icon={() => <StyledEditIcon />}
                size={IconButton.sizes.SMALL}
                kind={IconButton.kinds.TERTIARY}
                // ariaLabel='Edit'
              />
            </StyledTableButtons>
          )
        },
        minWidth: 80,
        width: 80,
        flex: 2,
      },
    ],
    [groups],
  )

  return (
    <StyledSectionWrapper>
      <StyledHeaderGroup className='header_group'>
        <div>
          <StyledSectionTitle>Groups</StyledSectionTitle>
          {/* <StyledSectionDescription>
            Here is your datasource, a collection of databases, APIs, files, and more.
          </StyledSectionDescription> */}
        </div>
        <div>
          <ButtonPrimary onClick={() => navigate('/groups/create-group')} size={'small'}>
            Add Group
          </ButtonPrimary>
        </div>
      </StyledHeaderGroup>

      <ComponentsWrapper>
        {/* <StyledCardsWrapper> */}
        <div>
          <DataGrid
            // ref={gridRef}
            data={gridData}
            columnConfig={config}
            headerHeight={130}
            maxHeight={310}
          />
        </div>
        {/* </StyledCardsWrapper> */}
      </ComponentsWrapper>
    </StyledSectionWrapper>
  )
}

export default Groups

export const StyledTableButtons = styled.div`
  display: flex;
  align-items: center;
`
