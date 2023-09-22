import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import styled from 'styled-components'

import Tab from '@l3-lib/ui-core/dist/Tab'
import TabList from '@l3-lib/ui-core/dist/TabList'
import TabPanel from '@l3-lib/ui-core/dist/TabPanel'
import TabPanels from '@l3-lib/ui-core/dist/TabPanels'
import TabsContext from '@l3-lib/ui-core/dist/TabsContext'
import IconButton from '@l3-lib/ui-core/dist/IconButton'

import Edit from '@l3-lib/ui-core/dist/icons/Edit'

import AvatarGenerator from 'components/AvatarGenerator/AvatarGenerator'

import AgentViewDetailBox from 'pages/Agents/AgentView/components/AgentViewDetailBox'
import TeamOfAgentsDetailsBox from 'pages/TeamOfAgents/components/TeamOfAgentsDetailsBox'

import { AuthContext } from 'contexts'

import EyeOpen from '@l3-lib/ui-core/dist/icons/EyeOpen'
import { useModal } from 'hooks'

const ChatMembers = ({
  agentById,
  teamOfAgents,
  userName,
}: {
  agentById?: any
  teamOfAgents?: any
  userName?: string
}) => {
  const { user } = React.useContext(AuthContext)

  const [activeTab, setActiveTab] = useState(0)

  const navigate = useNavigate()

  const { openModal } = useModal()

  if (agentById) {
    const isCreator = user?.id === agentById.agent?.created_by

    const handleEdit = () => {
      navigate(`/agents/${agentById.agent?.id}/edit-agent`)
    }

    return (
      <StyledRoot>
        <TabList size='small'>
          <Tab onClick={() => setActiveTab(0)}>Members</Tab>
          <Tab onClick={() => setActiveTab(1)}>Info</Tab>
        </TabList>

        <StyledContainer>
          <TabsContext activeTabId={activeTab}>
            <TabPanels noAnimation>
              <TabPanel>
                {userName && (
                  <StyledAgentWrapper>
                    <AvatarGenerator name={userName} size={30} />
                    {userName}
                  </StyledAgentWrapper>
                )}

                <>
                  <StyledAgentWrapper>
                    <AvatarGenerator name={agentById?.agent?.name} size={30} />
                    {agentById?.agent?.name}

                    <StyledIconButtonWrapper className='hiddenButton'>
                      <IconButton
                        onClick={() =>
                          openModal({
                            name: 'agent-view-modal',
                            data: {
                              agent: agentById,
                            },
                          })
                        }
                        icon={() => (
                          <StyledIconWrapper>
                            <EyeOpen size={50} />
                          </StyledIconWrapper>
                        )}
                        size={IconButton.sizes.SMALL}
                        kind={IconButton.kinds.TERTIARY}
                        // ariaLabel='View'
                      />

                      {isCreator && (
                        <IconButton
                          onClick={handleEdit}
                          icon={() => <Edit />}
                          size={IconButton.sizes.SMALL}
                          kind={IconButton.kinds.TERTIARY}
                          // ariaLabel='Edit'
                        />
                      )}
                    </StyledIconButtonWrapper>
                  </StyledAgentWrapper>
                </>
              </TabPanel>

              <TabPanel>
                <AgentViewDetailBox agentData={agentById} />
              </TabPanel>
            </TabPanels>
          </TabsContext>
        </StyledContainer>
      </StyledRoot>
    )
  }

  if (teamOfAgents) {
    return (
      <StyledRoot>
        <TabList size='small'>
          <Tab onClick={() => setActiveTab(0)}>Members</Tab>
          <Tab onClick={() => setActiveTab(1)}>Info</Tab>
        </TabList>

        <StyledContainer>
          <TabsContext activeTabId={activeTab}>
            <TabPanels noAnimation>
              <TabPanel>
                {userName && (
                  <StyledAgentWrapper>
                    <AvatarGenerator name={userName} size={30} />
                    {userName}
                  </StyledAgentWrapper>
                )}

                {teamOfAgents &&
                  teamOfAgents.team_agents?.map((agentData: any, index: number) => {
                    const handleEdit = () => {
                      navigate(`/agents/${agentData.agent?.id}/edit-agent`)
                    }

                    const isCreator = user?.id === agentData.agent?.created_by

                    return (
                      <StyledAgentWrapper key={index}>
                        <AvatarGenerator name={agentData.agent.name} size={30} />
                        {agentData.agent.name}

                        <StyledIconButtonWrapper className='hiddenButton'>
                          <IconButton
                            onClick={() =>
                              openModal({
                                name: 'agent-view-modal',
                                data: {
                                  agent: {
                                    agent: agentData.agent,
                                    configs: {
                                      tools: [],
                                      goals: [],
                                      constraints: [],
                                      instructions: [],
                                      datasources: [],
                                      suggestions: [],
                                      greeting: [],
                                    },
                                  },
                                },
                              })
                            }
                            icon={() => (
                              <StyledIconWrapper>
                                <EyeOpen size={50} />
                              </StyledIconWrapper>
                            )}
                            size={IconButton.sizes.SMALL}
                            kind={IconButton.kinds.TERTIARY}
                            // ariaLabel='View'
                          />

                          {isCreator && (
                            <IconButton
                              onClick={handleEdit}
                              icon={() => <Edit />}
                              size={IconButton.sizes.SMALL}
                              kind={IconButton.kinds.TERTIARY}
                              // ariaLabel='Edit'
                            />
                          )}
                        </StyledIconButtonWrapper>
                      </StyledAgentWrapper>
                    )
                  })}
              </TabPanel>

              <TabPanel>
                <TeamOfAgentsDetailsBox teamData={teamOfAgents} />
              </TabPanel>
            </TabPanels>
          </TabsContext>
        </StyledContainer>
      </StyledRoot>
    )
  }

  return <div />
}

export default ChatMembers

const StyledRoot = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;

  gap: 10px;
`

const StyledContainer = styled.div`
  overflow-y: auto;
`

const StyledAgentWrapper = styled.div`
  display: flex;
  align-items: center;
  gap: 5px;

  padding: 10px;
  width: 300px;

  padding-left: 15px;
  border-radius: 10px;

  :hover {
    background: rgba(0, 0, 0, 0.1);
    .hiddenButton {
      opacity: 1;
    }
  }
`
const StyledIconWrapper = styled.div`
  color: transparent;
`
const StyledIconButtonWrapper = styled.div`
  margin-left: auto;

  opacity: 0;
  /* transition: opacity 300ms; */

  display: flex;
  align-items: center;
`
