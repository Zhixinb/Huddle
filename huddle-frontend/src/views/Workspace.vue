<template>
    <div>
    <v-navigation-drawer app>
        <v-list-item v-for="s in slides" :key="s.message" link @click.stop="update_slide(s.id)">
            <v-list-item-content>
                <slide :message="s.message"> </slide>
            </v-list-item-content>
        </v-list-item>
    </v-navigation-drawer>

    <v-app-bar app>

        <v-toolbar-title>Huddle: {{ curr_slide_id }} </v-toolbar-title>
        <v-spacer></v-spacer>
        <v-tooltip bottom>
             <template v-slot:activator="{ on, attrs }">
                <v-btn icon v-bind="attrs" v-on="on" id="text_box">
                    <!-- <v-icon>mdi-vector-square</v-icon> -->
                </v-btn>
             </template>
             <span>New Textbox</span>
        </v-tooltip>
        <v-tooltip bottom>
             <template v-slot:activator="{ on, attrs }">
                <v-btn icon v-bind="attrs" v-on="on" @click.stop="append_slide">
                    <v-icon>mdi-plus</v-icon>
                </v-btn>
             </template>
             <span>New Slide</span>
        </v-tooltip>
    </v-app-bar>

    <div class="pa-5">
        <v-fade-transition appear>
            <v-card width=125vh height=70.3125vh>
                <div id="graph-wrapper"></div>
            </v-card>
        </v-fade-transition>
    </div>

    </div>
</template>

<script>
import Slide from '@/components/app/Slide';
import {mapState} from 'vuex';

var graph;

export default {
    name: 'Workspace',
    data() {
        return {
            curr_slide_id: 0,
            slides: [
                { id: 0, message: '0' }
            ]
        }
    },
    mounted() {
        this.draw();
    },
    methods:
    {
        update_slide(id) {
            this.load_slide();
            graph.getModel().clear();
            this.curr_slide_id = id;
            var xml = this.slides[this.curr_slide_id].message;
            var doc = mxUtils.parseXml(xml);
            var codec = new mxCodec(doc);
            codec.decode(doc.documentElement, graph.getModel());
            var elt = doc.documentElement.firstChild;
            var cells = [];

            while (elt != null) {
                cells.push(codec.decode(elt));
                elt = elt.nextSibling;
            }

            graph.addCells(cells);
        },
        load_slide() {
            var encoder = new mxCodec();
            var result = encoder.encode(graph.getModel());
            var xml = mxUtils.getXml(result);
            this.slides[this.curr_slide_id].message = xml;
        },
        append_slide() {
            this.load_slide();
            this.slides.push({ id: this.slides.length, message: this.slides.length });
        },
        draw()
        {
            if (!mxClient.isBrowserSupported()) {
                mxUtils.error("Browser is not supported!", 200, false);
            } else {
                // new toolbar without event processing
                var toolbar = new mxToolbar(document.getElementById("text_box"));
                toolbar.enabled = false;

                // the div for the graph
                var container = document.createElement("div");   
                container.id = "grid" // KS: add an Id so we can find it later
                container.style.position = "absolute";
                container.style.overflow = "hidden";
                container.style.left = "0px";
                container.style.top = "0px";
                container.style.right = "0px";
                container.style.bottom = "0px";
                container.style.background =
                'url("https://jgraph.github.io/mxgraph/javascript/examples/editors/images/grid.gif")';

                document.getElementById("graph-wrapper").appendChild(container);

                // creates the model and the graph inside the container
                var model = new mxGraphModel();
                graph = new mxGraph(container, model);

                graph.setConnectable(false);
                graph.setMultigraph(false);

                var addVertex = function(icon, w, h, style) {
                    var vertex = new mxCell(null, new mxGeometry(0, 0, w, h), style);
                    vertex.setVertex(true);

                    var funct = function(graph, evt, cell, x, y) {
                        graph.stopEditing(false);

                        var v = graph.getModel().cloneCell(vertex);
                        v.geometry.x = x;
                        v.geometry.y = y;

                        graph.addCell(v);
                        graph.setSelectionCell(v);
                    };

                    // Creates the image which is used as the drag icon (preview)
                    var img = toolbar.addMode(null, icon, function(evt, cell) {
                        var pt = this.graph.getPointForEvent(evt);
                        funct(graph, evt, cell, pt.x, pt.y);
                    });

                    mxEvent.addListener(img, "mousedown", function(evt) {
                        if (img.enabled == false) {
                        mxEvent.consume(evt);
                        }
                    });

                    mxUtils.makeDraggable(img, graph, funct);

                    graph.getSelectionModel().addListener(mxEvent.CHANGE, function() {
                        var tmp = graph.isSelectionEmpty();
                        mxUtils.setOpacity(img, tmp ? 100 : 20);
                        img.enabled = tmp;
                    });
                };

                addVertex("https://jgraph.github.io/mxgraph/javascript/examples/editors/images/rounded.gif", 100, 40, "shape=rounded");
            }
        }
    },
    components: {
        Slide
    },
    computed: {
        ...mapState(['workspace'])
    }
}
</script>
