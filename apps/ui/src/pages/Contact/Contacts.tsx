import { useNavigate } from 'react-router-dom'

import { ButtonPrimary } from 'components/Button/Button'
import ComponentsWrapper from 'components/ComponentsWrapper/ComponentsWrapper'

import { StyledCardsWrapper } from 'pages/Agents/Agents'

import IconButton from '@l3-lib/ui-core/dist/IconButton'

import {
  StyledHeaderGroup,
  StyledSectionTitle,
  StyledSectionWrapper,
} from 'pages/Home/homeStyle.css'
import { useContacts } from './useContacts'
import TempCard from 'pages/Group/TempCard'
import { StyledTableButtons } from 'pages/Group/Groups'
import HeaderComponent from 'components/DataGrid/GridComponents/HeaderComponent'
import TextCellRenderer from 'pages/TeamOfAgents/TeamOfAgentsTable/TextCellRenderer'
import {
  StyledDeleteIcon,
  StyledEditIcon,
} from 'pages/TeamOfAgents/TeamOfAgentsCard/TeamOfAgentsCard'
import DataGrid from 'components/DataGrid'
import { useMemo } from 'react'

const Contacts = () => {
  const navigate = useNavigate()

  const { contacts, deleteContactHandler } = useContacts()

  const gridData =
    contacts?.map((contact: any) => ({
      id: contact.id,
      name: contact.name,
      description: contact.description,
      email: contact.email,
      phone: contact.phone,
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
        width: 200,
        flex: 2,
      },
      {
        headerName: 'Description',
        field: 'description',
        headerComponent: HeaderComponent,
        resizable: true,
        cellRenderer: TextCellRenderer,
        minWidth: 200,
        width: 200,
        flex: 2,
      },
      {
        headerName: 'Email',
        field: 'email',
        headerComponent: HeaderComponent,
        resizable: true,
        cellRenderer: TextCellRenderer,
        minWidth: 200,
        width: 200,
        // flex: 2,
      },
      {
        headerName: 'Phone',
        field: 'phone',
        headerComponent: HeaderComponent,
        resizable: true,
        cellRenderer: TextCellRenderer,
        minWidth: 200,
        width: 200,
        // flex: 2,
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
                onClick={() => deleteContactHandler(id)}
                icon={() => <StyledDeleteIcon />}
                size={IconButton.sizes.SMALL}
                kind={IconButton.kinds.TERTIARY}
                // ariaLabel='Delete'
              />

              <IconButton
                onClick={() => navigate(`/contacts/${id}/edit-contact`)}
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
    [contacts],
  )

  return (
    <StyledSectionWrapper>
      <StyledHeaderGroup className='header_group'>
        <div>
          <StyledSectionTitle>Contacts</StyledSectionTitle>
          {/* <StyledSectionDescription>
          Here is your datasource, a collection of databases, APIs, files, and more.
        </StyledSectionDescription> */}
        </div>
        <div>
          <ButtonPrimary onClick={() => navigate('/contacts/create-contact')} size={'small'}>
            Add Contact
          </ButtonPrimary>
        </div>
      </StyledHeaderGroup>

      <ComponentsWrapper>
        <div>
          <DataGrid
            // ref={gridRef}
            data={gridData}
            columnConfig={config}
            headerHeight={130}
            maxHeight={310}
          />
        </div>
      </ComponentsWrapper>
    </StyledSectionWrapper>
  )
}

export default Contacts
